from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel, Field


class AccountStatus(BaseModel):
    status: str = Field(alias="Status")
    account_name: str = Field(alias="AccountName")
    remaind_credit: float = Field(alias="RemaindCredit")
    mobile: str = Field(alias="Mobile")
    expire_date: str = Field(alias="ExpireDate")
    expire_date_per: str = Field(alias="ExpireDatePer")


class QuickSendResponse(BaseModel):
    error_code: int = Field(alias="ErrorCode")
    quick_send_id: Optional[int] = Field(alias="QuickSendID")
    generated_code: Optional[str] = Field(alias="GeneratedCode")


class UploadMessageResponse(BaseModel):
    id: int = Field(alias="Id")
    length: int = Field(alias="Length")


class GenerateTTSResponse(BaseModel):
    id: int = Field(alias="Id")
    length: int = Field(alias="Length")


class QuickSendResult(BaseModel):
    result: int


class CreateCampaignResponse(BaseModel):
    result: int


class GetQuickSendResponse(BaseModel):
    reason: int
    status: str
    dst: str
    starttime: str
    id: int = Field(alias="Id")
    subscribeid: int
    duration: int
    vote: int


class StartCampaignResponse(BaseModel):
    result: int


class StopCampaignResponse(BaseModel):
    result: bool


class DeleteMessageResponse(BaseModel):
    result: bool


class AvanakClient:
    BASE_URL = "https://portal.avanak.ir/Rest"

    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": token})

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def account_status(self) -> AccountStatus:
        data = {}
        result = self._post("AccountStatus", data)
        return AccountStatus(**result)

    def send_otp(
        self, length: int, number: str, optional_code: int = 0, server_id: int = 0
    ) -> QuickSendResponse:
        data = {
            "Length": length,
            "Number": number,
            "OptionalCode": optional_code,
            "ServerID": server_id,
        }
        result = self._post("SendOTP", data)
        return QuickSendResponse(**result)

    def upload_message_base64(
        self,
        title: str,
        base64: str,
        persist: bool = False,
        call_from_mobile: Optional[str] = None,
    ) -> UploadMessageResponse:
        data = {
            "Title": title,
            "Base64": base64,
            "Persist": str(persist).lower(),
        }
        if call_from_mobile:
            data["CallFromMobile"] = call_from_mobile
        result = self._post("UploadMessageBase64", data)
        return UploadMessageResponse(**result)

    def generate_tts(
        self,
        text: str,
        title: str,
        speaker: str = "male",
        call_from_mobile: Optional[str] = None,
    ) -> GenerateTTSResponse:
        data = {
            "Text": text,
            "Title": title,
            "Speaker": speaker,
        }
        if call_from_mobile:
            data["CallFromMobile"] = call_from_mobile
        result = self._post("GenerateTTS", data)
        return GenerateTTSResponse(**result)

    def quick_send(
        self,
        message_id: int,
        number: str,
        vote: bool = False,
        server_id: int = 0,
        record_voice: bool = False,
        record_voice_duration: Optional[int] = None,
    ) -> dict:
        data = {
            "MessageID": message_id,
            "Number": number,
            "Vote": str(vote).lower(),
            "ServerID": server_id,
        }
        if record_voice:
            data["RecordVoice"] = str(record_voice).lower()
            if record_voice_duration:
                data["RecordVoiceDuration"] = record_voice_duration
        return self._post("QuickSend", data)

    def quick_send_with_tts(
        self,
        text: str,
        number: str,
        vote: bool = False,
        server_id: int = 0,
        call_from_mobile: Optional[str] = None,
        record_voice: bool = False,
        record_voice_duration: Optional[int] = None,
    ) -> dict:
        data = {
            "Text": text,
            "Number": number,
            "Vote": str(vote).lower(),
            "ServerID": server_id,
        }
        if call_from_mobile:
            data["CallFromMobile"] = call_from_mobile
        if record_voice:
            data["RecordVoice"] = str(record_voice).lower()
            if record_voice_duration:
                data["RecordVoiceDuration"] = record_voice_duration
        return self._post("QuickSendWithTTS", data)

    def create_campaign(
        self,
        title: str,
        numbers: str,
        message_id: int,
        start_date_time: str,
        end_date_time: str,
        max_try_count: int = 1,
        minute_between_tries: int = 10,
        server_id: int = 0,
        auto_start: bool = True,
        vote: bool = False,
        sms: bool = False,
        sms_json: Optional[str] = None,
        priority: int = 0,
    ) -> CreateCampaignResponse:
        data = {
            "Title": title,
            "Numbers": numbers,
            "MessageID": message_id,
            "StartDateTime": start_date_time,
            "EndDateTime": end_date_time,
            "MaxTryCount": max_try_count,
            "MinuteBetweenTries": minute_between_tries,
            "ServerID": server_id,
            "AutoStart": str(auto_start).lower(),
            "Vote": str(vote).lower(),
            "SMS": str(sms).lower(),
            "Priority": priority,
        }
        if sms_json:
            data["SMSJSON"] = sms_json
        result = self._post("CreateCampaign", data)
        try:
            return CreateCampaignResponse(result=result["result"])
        except (KeyError, TypeError):
            return CreateCampaignResponse(result=result)

    def get_quick_send(self, quick_send_id: int) -> Optional[GetQuickSendResponse]:
        data = {"QuickSendID": quick_send_id}
        result = self._post("GetQuickSend", data)
        if result is None:
            return None
        return GetQuickSendResponse(**result)

    def download_message(self, message_id: int) -> bytes:
        data = {"MessageID": message_id}
        url = f"{self.BASE_URL}/DownloadMessage"
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.content

    def start_campaign(
        self,
        campaign_id: int,
        start_date_time: str,
        end_date_time: str,
        max_try_count: int = 1,
        minute_between_tries: int = 10,
        title: Optional[str] = None,
        server_id: int = 0,
    ) -> StartCampaignResponse:
        data = {
            "CampaignID": campaign_id,
            "StartDateTime": start_date_time,
            "EndDateTime": end_date_time,
            "MaxTryCount": max_try_count,
            "MinuteBetweenTries": minute_between_tries,
            "ServerID": server_id,
        }
        if title:
            data["Title"] = title
        result = self._post("StartCampaign", data)
        try:
            return StartCampaignResponse(result=result["result"])
        except (KeyError, TypeError):
            return StartCampaignResponse(result=result)

    def stop_campaign(self, campaign_id: int) -> StopCampaignResponse:
        data = {"CampaignID": campaign_id}
        result = self._post("StopCampaign", data)
        try:
            return StopCampaignResponse(result=result["result"])
        except (KeyError, TypeError):
            return StopCampaignResponse(result=result)

    def get_campaign(self, campaign_id: int) -> Dict[str, Any]:
        data = {"CampaignID": campaign_id}
        return self._post("GetCampaign", data)

    def get_campaign_numbers_by_campaign_id(self, campaign_id: int) -> Dict[str, Any]:
        data = {"CampaignID": campaign_id}
        return self._post("GetCampaignNumbersByCampaignID", data)

    def get_message(self, message_id: int) -> Dict[str, Any]:
        data = {"MessageID": message_id}
        return self._post("GetMessage", data)

    def delete_message(self, message_id: int) -> DeleteMessageResponse:
        data = {"MessageID": message_id}
        result = self._post("DeleteMessage", data)
        try:
            return DeleteMessageResponse(result=result["result"])
        except (KeyError, TypeError):
            return DeleteMessageResponse(result=result)

    def get_messages(self, skip: int = 0, take: Optional[int] = None) -> Dict[str, Any]:
        data = {"Skip": skip}
        if take:
            data["Take"] = take
        return self._post("GetMessages", data)

    def get_quick_send_statistics(self, start_date_time: str, end_date_time: str) -> Dict[str, Any]:
        data = {
            "StartDateTime": start_date_time,
            "EndDateTime": end_date_time,
        }
        return self._post("GetQuickSendStatistics", data)
