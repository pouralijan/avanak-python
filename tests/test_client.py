from unittest.mock import Mock, patch

import pytest

from avanak import AvanakClient


class TestAvanakClient:
    @pytest.fixture
    def client(self):
        return AvanakClient(token="test_token")

    @pytest.fixture
    def mock_session(self, client):
        with patch.object(client, "session") as mock_session:
            yield mock_session

    def test_init(self):
        client = AvanakClient(token="test_token")
        assert client.token == "test_token"
        assert client.BASE_URL == "https://portal.avanak.ir/Rest"

    def test_account_status(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Status": "Success",
            "AccountName": "Test Account",
            "RemaindCredit": 1000.0,
            "Mobile": "09120000000",
            "ExpireDate": "2025-12-31",
            "ExpireDatePer": "1404/10/10",
        }
        mock_session.post.return_value = mock_response

        result = client.account_status()

        assert result.status == "Success"
        assert result.account_name == "Test Account"
        assert result.remaind_credit == 1000.0
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/AccountStatus", data={}
        )

    def test_send_otp(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "ErrorCode": 0,
            "QuickSendID": 12345,
            "GeneratedCode": "1234",
        }
        mock_session.post.return_value = mock_response

        result = client.send_otp(length=4, number="09120000000")

        assert result.error_code == 0
        assert result.quick_send_id == 12345
        assert result.generated_code == "1234"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/SendOTP",
            data={"Length": 4, "Number": "09120000000", "OptionalCode": 0, "ServerID": 0},
        )

    def test_upload_message_base64(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"Id": 12345, "Length": 30}
        mock_session.post.return_value = mock_response

        result = client.upload_message_base64(
            title="Test Message", base64="base64data", persist=True, call_from_mobile="09120000000"
        )

        assert result.id == 12345
        assert result.length == 30
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/UploadMessageBase64",
            data={
                "Title": "Test Message",
                "Base64": "base64data",
                "Persist": "true",
                "CallFromMobile": "09120000000",
            },
        )

    def test_generate_tts(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"Id": 12345, "Length": 25}
        mock_session.post.return_value = mock_response

        result = client.generate_tts(
            text="Hello World", title="Test TTS", speaker="male", call_from_mobile="09120000000"
        )

        assert result.id == 12345
        assert result.length == 25
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GenerateTTS",
            data={
                "Text": "Hello World",
                "Title": "Test TTS",
                "Speaker": "male",
                "CallFromMobile": "09120000000",
            },
        )

    def test_quick_send(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "QuickSendID": 12345,
            "MessageID": 67890,
            "MessageLength": 30,
            "CreditDecrease_InSeconds": 30,
            "CreditDecrease_InPulses": 1,
            "CreditDecrease_InPrice": 1350,
            "Status": "Success",
        }
        mock_session.post.return_value = mock_response

        result = client.quick_send(
            message_id=67890,
            number="09120000000",
            vote=True,
            server_id=1,
            record_voice=True,
            record_voice_duration=60,
        )

        assert result["QuickSendID"] == 12345
        assert result["Status"] == "Success"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/QuickSend",
            data={
                "MessageID": 67890,
                "Number": "09120000000",
                "Vote": "true",
                "ServerID": 1,
                "RecordVoice": "true",
                "RecordVoiceDuration": 60,
            },
        )

    def test_quick_send_with_tts(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "QuickSendID": 12345,
            "MessageID": 67890,
            "MessageLength": 25,
            "CreditDecrease_InSeconds": 25,
            "CreditDecrease_InPulses": 1,
            "CreditDecrease_InPrice": 1125,
            "Status": "Success",
        }
        mock_session.post.return_value = mock_response

        result = client.quick_send_with_tts(
            text="Hello World",
            number="09120000000",
            vote=False,
            server_id=0,
            call_from_mobile="09120000000",
            record_voice=False,
        )

        assert result["QuickSendID"] == 12345
        assert result["Status"] == "Success"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/QuickSendWithTTS",
            data={
                "Text": "Hello World",
                "Number": "09120000000",
                "Vote": "false",
                "ServerID": 0,
                "CallFromMobile": "09120000000",
            },
        )

    def test_create_campaign(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"result": 12345}
        mock_session.post.return_value = mock_response

        result = client.create_campaign(
            title="Test Campaign",
            numbers="09120000000,09130000000",
            message_id=67890,
            start_date_time="2024-01-01 10:00:00",
            end_date_time="2024-01-01 18:00:00",
            max_try_count=3,
            minute_between_tries=15,
            server_id=1,
            auto_start=False,
            vote=True,
            sms=True,
            sms_json='[{"SMSType": "Success", "MessageText": "Done", "LineNumber": "public", "HasBackupLine": true}]',
            priority=5,
        )

        assert result.result == 12345
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/CreateCampaign",
            data={
                "Title": "Test Campaign",
                "Numbers": "09120000000,09130000000",
                "MessageID": 67890,
                "StartDateTime": "2024-01-01 10:00:00",
                "EndDateTime": "2024-01-01 18:00:00",
                "MaxTryCount": 3,
                "MinuteBetweenTries": 15,
                "ServerID": 1,
                "AutoStart": "false",
                "Vote": "true",
                "SMS": "true",
                "Priority": 5,
                "SMSJSON": '[{"SMSType": "Success", "MessageText": "Done", "LineNumber": "public", "HasBackupLine": true}]',
            },
        )

    def test_get_quick_send(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "reason": 0,
            "status": "Delivered",
            "dst": "09120000000",
            "starttime": "2024-01-01 10:00:00",
            "Id": 12345,
            "subscribeid": 12345,
            "duration": 30,
            "vote": 1,
        }
        mock_session.post.return_value = mock_response

        result = client.get_quick_send(quick_send_id=12345)

        assert result is not None
        assert result.reason == 0
        assert result.status == "Delivered"
        assert result.id == 12345
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetQuickSend", data={"QuickSendID": 12345}
        )

    def test_get_quick_send_none(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = None
        mock_session.post.return_value = mock_response

        result = client.get_quick_send(quick_send_id=12345)

        assert result is None

    def test_download_message(self, client, mock_session):
        mock_response = Mock()
        mock_response.content = b"audio_data"
        mock_session.post.return_value = mock_response

        result = client.download_message(message_id=67890)

        assert result == b"audio_data"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/DownloadMessage", data={"MessageID": 67890}
        )

    def test_start_campaign(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"result": 12345}
        mock_session.post.return_value = mock_response

        result = client.start_campaign(
            campaign_id=12345,
            start_date_time="2024-01-01 10:00:00",
            end_date_time="2024-01-01 18:00:00",
            max_try_count=2,
            minute_between_tries=20,
            title="Updated Campaign",
            server_id=2,
        )

        assert result.result == 12345
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/StartCampaign",
            data={
                "CampaignID": 12345,
                "StartDateTime": "2024-01-01 10:00:00",
                "EndDateTime": "2024-01-01 18:00:00",
                "MaxTryCount": 2,
                "MinuteBetweenTries": 20,
                "Title": "Updated Campaign",
                "ServerID": 2,
            },
        )

    def test_stop_campaign(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"result": True}
        mock_session.post.return_value = mock_response

        result = client.stop_campaign(campaign_id=12345)

        assert result.result is True
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/StopCampaign", data={"CampaignID": 12345}
        )

    def test_get_campaign(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "CampaignID": 12345,
            "Title": "Test Campaign",
            "Status": "Running",
        }
        mock_session.post.return_value = mock_response

        result = client.get_campaign(campaign_id=12345)

        assert result["CampaignID"] == 12345
        assert result["Title"] == "Test Campaign"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetCampaign", data={"CampaignID": 12345}
        )

    def test_get_campaign_numbers_by_campaign_id(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Numbers": ["09120000000", "09130000000"],
            "Status": "Success",
        }
        mock_session.post.return_value = mock_response

        result = client.get_campaign_numbers_by_campaign_id(campaign_id=12345)

        assert result["Numbers"] == ["09120000000", "09130000000"]
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetCampaignNumbersByCampaignID",
            data={"CampaignID": 12345},
        )

    def test_get_message(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Details": {
                "Id": 67890,
                "Title": "Test Message",
                "Lenght": 30,
                "IsDefault": False,
                "ShowInGallery": True,
                "Confirmed": 1,
                "CreateDate": "2024-01-01T10:00:00",
                "InternalPrice": 0,
                "ExternalPrice": 1350,
            },
            "Status": "Success",
        }
        mock_session.post.return_value = mock_response

        result = client.get_message(message_id=67890)

        assert result["Details"]["Id"] == 67890
        assert result["Details"]["Title"] == "Test Message"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetMessage", data={"MessageID": 67890}
        )

    def test_delete_message(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"result": True}
        mock_session.post.return_value = mock_response

        result = client.delete_message(message_id=67890)

        assert result.result is True
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/DeleteMessage", data={"MessageID": 67890}
        )

    def test_get_messages(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Messages": [{"Id": 67890, "Title": "Message 1"}, {"Id": 67891, "Title": "Message 2"}],
            "TotalCount": 2,
        }
        mock_session.post.return_value = mock_response

        result = client.get_messages(skip=0, take=10)

        assert len(result["Messages"]) == 2
        assert result["Messages"][0]["Title"] == "Message 1"
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetMessages", data={"Skip": 0, "Take": 10}
        )

    def test_get_messages_no_take(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Messages": [{"Id": 67890, "Title": "Message 1"}],
            "TotalCount": 1,
        }
        mock_session.post.return_value = mock_response

        result = client.get_messages(skip=5)

        assert len(result["Messages"]) == 1
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetMessages", data={"Skip": 5}
        )

    def test_get_quick_send_statistics(self, client, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {
            "TotalSent": 100,
            "TotalDelivered": 95,
            "TotalFailed": 5,
            "Statistics": [],
        }
        mock_session.post.return_value = mock_response

        result = client.get_quick_send_statistics(
            start_date_time="2024-01-01", end_date_time="2024-01-31"
        )

        assert result["TotalSent"] == 100
        assert result["TotalDelivered"] == 95
        mock_session.post.assert_called_once_with(
            "https://portal.avanak.ir/Rest/GetQuickSendStatistics",
            data={"StartDateTime": "2024-01-01", "EndDateTime": "2024-01-31"},
        )
