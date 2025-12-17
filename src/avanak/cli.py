import os
from pathlib import Path

import click

from .client import AvanakClient


def get_token():
    """Get token from environment, file, or prompt."""
    token_file = Path.home() / ".avanak_token"

    # Check environment variable
    token = os.getenv("AVANAK_TOKEN")
    if token:
        return token

    # Check file
    if token_file.exists():
        return token_file.read_text().strip()

    # Prompt
    token = click.prompt("Enter your Avanak API token", hide_input=True)
    save = click.confirm("Save token to file for future use?", default=True)
    if save:
        token_file.write_text(token)
        token_file.chmod(0o600)  # Secure permissions
    return token


@click.group()
@click.pass_context
def cli(ctx):
    """Avanak API CLI tool."""
    token = get_token()
    ctx.ensure_object(dict)
    ctx.obj["client"] = AvanakClient(token=token)


@cli.command()
@click.pass_context
def account_status(ctx):
    """Get account status."""
    client = ctx.obj["client"]
    try:
        status = client.account_status()
        click.echo(f"Account Name: {status.account_name}")
        click.echo(f"Remaining Credit: {status.remaind_credit} Rials")
        click.echo(f"Expire Date: {status.expire_date}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("length", type=int, default=4)
@click.argument("number")
@click.pass_context
def send_otp(ctx, length, number):
    """Send OTP to a number."""
    client = ctx.obj["client"]
    try:
        response = client.send_otp(length=length, number=number)
        click.echo(f"Error Code: {response.error_code}")
        click.echo(f"Quick Send ID: {response.quick_send_id}")
        click.echo(f"Generated Code: {response.generated_code}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("title")
@click.argument("base64_file")
@click.option("--persist", is_flag=True)
@click.option("--call-from-mobile")
@click.pass_context
def upload_message(ctx, title, base64_file, persist, call_from_mobile):
    """Upload a base64 encoded audio file."""
    import base64

    client = ctx.obj["client"]
    try:
        with Path(base64_file).open("rb") as f:
            data = base64.b64encode(f.read()).decode()
        response = client.upload_message_base64(
            title=title, base64=data, persist=persist, call_from_mobile=call_from_mobile
        )
        click.echo(f"Message ID: {response.id}")
        click.echo(f"Length: {response.length} seconds")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("text")
@click.argument("title")
@click.option("--speaker", default="male")
@click.option("--call-from-mobile")
@click.pass_context
def generate_tts(ctx, text, title, speaker, call_from_mobile):
    """Generate TTS audio."""
    client = ctx.obj["client"]
    try:
        response = client.generate_tts(
            text=text, title=title, speaker=speaker, call_from_mobile=call_from_mobile
        )
        click.echo(f"Message ID: {response.id}")
        click.echo(f"Length: {response.length} seconds")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("message_id", type=int)
@click.argument("number")
@click.option("--vote", is_flag=True)
@click.option("--server-id", type=int, default=0)
@click.pass_context
def quick_send(ctx, message_id, number, vote, server_id):
    """Send a quick voice message."""
    client = ctx.obj["client"]
    try:
        response = client.quick_send(
            message_id=message_id, number=number, vote=vote, server_id=server_id
        )
        click.echo(f"Send Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("text")
@click.argument("number")
@click.option("--vote", is_flag=True)
@click.option("--server-id", type=int, default=0)
@click.option("--call-from-mobile")
@click.pass_context
def quick_send_tts(ctx, text, number, vote, server_id, call_from_mobile):
    """Send a quick TTS message."""
    client = ctx.obj["client"]
    try:
        response = client.quick_send_with_tts(
            text=text,
            number=number,
            vote=vote,
            server_id=server_id,
            call_from_mobile=call_from_mobile,
        )
        click.echo(f"Send Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("title")
@click.argument("numbers")  # comma separated
@click.argument("message_id", type=int)
@click.argument("start_date_time")
@click.argument("end_date_time")
@click.option("--max-try-count", type=int, default=1)
@click.option("--minute-between-tries", type=int, default=10)
@click.option("--server-id", type=int, default=0)
@click.option("--auto-start", is_flag=True, default=True)
@click.option("--vote", is_flag=True)
@click.pass_context
def create_campaign(
    ctx,
    title,
    numbers,
    message_id,
    start_date_time,
    end_date_time,
    max_try_count,
    minute_between_tries,
    server_id,
    auto_start,
    vote,
):
    """Create a campaign."""
    client = ctx.obj["client"]
    try:
        response = client.create_campaign(
            title=title,
            numbers=numbers,
            message_id=message_id,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            max_try_count=max_try_count,
            minute_between_tries=minute_between_tries,
            server_id=server_id,
            auto_start=auto_start,
            vote=vote,
        )
        click.echo(f"Campaign Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("quick_send_id", type=int)
@click.pass_context
def get_quick_send(ctx, quick_send_id):
    """Get quick send status."""
    client = ctx.obj["client"]
    try:
        response = client.get_quick_send(quick_send_id=quick_send_id)
        if response:
            click.echo(f"Quick Send: {response}")
        else:
            click.echo("Not found")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("message_id", type=int)
@click.argument("output_file")
@click.pass_context
def download_message(ctx, message_id, output_file):
    """Download a message."""
    client = ctx.obj["client"]
    try:
        data = client.download_message(message_id=message_id)
        with Path(output_file).open("wb") as f:
            f.write(data)
        click.echo(f"Downloaded to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("campaign_id", type=int)
@click.argument("start_date_time")
@click.argument("end_date_time")
@click.option("--max-try-count", type=int, default=1)
@click.option("--minute-between-tries", type=int, default=10)
@click.option("--title")
@click.option("--server-id", type=int, default=0)
@click.pass_context
def start_campaign(
    ctx,
    campaign_id,
    start_date_time,
    end_date_time,
    max_try_count,
    minute_between_tries,
    title,
    server_id,
):
    """Start a campaign."""
    client = ctx.obj["client"]
    try:
        response = client.start_campaign(
            campaign_id=campaign_id,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            max_try_count=max_try_count,
            minute_between_tries=minute_between_tries,
            title=title,
            server_id=server_id,
        )
        click.echo(f"Start Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("campaign_id", type=int)
@click.pass_context
def stop_campaign(ctx, campaign_id):
    """Stop a campaign."""
    client = ctx.obj["client"]
    try:
        response = client.stop_campaign(campaign_id=campaign_id)
        click.echo(f"Stop Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("campaign_id", type=int)
@click.pass_context
def get_campaign(ctx, campaign_id):
    """Get campaign details."""
    client = ctx.obj["client"]
    try:
        response = client.get_campaign(campaign_id=campaign_id)
        click.echo(f"Campaign: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("campaign_id", type=int)
@click.pass_context
def get_campaign_numbers(ctx, campaign_id):
    """Get campaign numbers."""
    client = ctx.obj["client"]
    try:
        response = client.get_campaign_numbers_by_campaign_id(campaign_id=campaign_id)
        click.echo(f"Numbers: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("message_id", type=int)
@click.pass_context
def get_message(ctx, message_id):
    """Get message details."""
    client = ctx.obj["client"]
    try:
        response = client.get_message(message_id=message_id)
        click.echo(f"Message: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("message_id", type=int)
@click.pass_context
def delete_message(ctx, message_id):
    """Delete a message."""
    client = ctx.obj["client"]
    try:
        response = client.delete_message(message_id=message_id)
        click.echo(f"Delete Result: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option("--skip", type=int, default=0)
@click.option("--take", type=int)
@click.pass_context
def get_messages(ctx, skip, take):
    """List messages."""
    client = ctx.obj["client"]
    try:
        response = client.get_messages(skip=skip, take=take)
        click.echo(f"Messages: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("start_date_time")
@click.argument("end_date_time")
@click.pass_context
def get_quick_send_statistics(ctx, start_date_time, end_date_time):
    """Get quick send statistics."""
    client = ctx.obj["client"]
    try:
        response = client.get_quick_send_statistics(
            start_date_time=start_date_time, end_date_time=end_date_time
        )
        click.echo(f"Statistics: {response}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
