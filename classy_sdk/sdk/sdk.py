from pathlib import Path
import uuid
import requests
from typing import Dict, List
from classy_sdk import ApiManager
from classy_sdk.utils import convert_image, join_url, validate_iso_datetime


class ClassySDK:
    """
    Queries Classy API endpoints.

    Args:
        source:
            A user/client name, e.g. 'dev.cz'.
        api_url (optional):
            A url to Classy API. It can be supplied
            as an argument or through environment variables.
        api_token (optional):
            An authorization token. It can be supplied
            as an argument or through environment variables.
        timeout (optional):
            A server response timeout in seconds, defaults to 30.

    Attributes:
        api:
            An instance of ApiManager to handle API setup and queries.
        source:
            A user/client name, e.g. 'dev.cz'.
        url:
            An API base url.

    Methods:
        list_cases:
            Retrieves a list of cases within an indicated time period.
        get_case:
            Retrieves one particular case.
        get_case_with_photos:
            Retrieves one particular case with photos.
        create_case:
            Creates a new case.
        update_case:
            Updates the case name as displayed in the Classy interface.
        delete_case:
            Marks the case to be deleted after a defined period.
        cancel_delete_case:
            Cancels the case deletion.
        postpone_delete_case:
            Postpones the case deletion to a requested timepoint.
        upload_photo:
            Uploads a photo in base64 format to the case.
        upload_photo_from_file:
            Uploads a photo file to the case.
        upload_pdf:
            Uploads a PDF in base64 format to the case.
        upload_pdf_from_file:
            Uploads a PDF file to the case.
        list_exports:
            Retrieves a list of performed exports.
        get_export:
            Retrieves one particular export.
        get_export_csv:
            Retrieves a csv file with requested export.
        get_export_download_url:
            Retrieves a csv download url for the requested export.
        list_inspections:
            Retrieves a list of performed inspections.
        get_inspection:
            Retrieves one particular inspection.
        get_inspection_with_photos:
            Retrieves one particular inspection with photos.
        create_inspection:
            Creates a new inspection.
        delete_inspection:
            Marks the inspection to be deleted after 3 days.
        cancel_delete_inspection:
            Cancels the inspection deletion.
        postpone_delete_inspection:
            Postpones the inspection deletion to a requested timepoint.
    """

    def __init__(
        self,
        source: str,
        api_url: str = None,
        api_token: str = None,
        timeout: int = 30,
    ) -> None:
        self.api = ApiManager(api_url, api_token, timeout)
        self.source = source
        self.url = self.api.api_url
        self._cases_url = "/cases"
        self._exports_url = "/exports"
        self._inspections_url = "/inspections"

    def list_cases(self, from_time: str, to_time: str) -> list:
        """Retrieves a list of cases within an indicated time period.

        Args:
            from_time:
                Start time, e.g. '2021-09-01T13:00:00.000Z'.
            to_time:
                End time, e.g. '2021-09-01T15:00:00.000Z'.

        Returns:
            A list of cases.
        """
        from_time = validate_iso_datetime(from_time)
        to_time = validate_iso_datetime(to_time)
        url = join_url(self.url, self._cases_url)
        params = {"from": from_time, "to": to_time, "source": self.source}
        return self.api.query("GET", url, params=params).json()

    def get_case(self, case_id: str) -> dict:
        """Retrieves one particular case.

        Atrs:
            case_id:
                A Searpent case id.

        Returns:
            Metadata related to the case.
        """
        url = join_url(self.url, self._cases_url, case_id)
        response = self.api.query("GET", url)
        return response.json()

    def get_case_with_photos(self, case_id: str) -> dict:
        """Retrieves one particular case with attached photos.

        Atrs:
            case_id:
                A Searpent case id.

        Returns:
            Metadata related to the case.
        """
        url = join_url(self.url, self._cases_url, case_id)
        params = {"withPhotos": "true"}
        response = self.api.query("GET", url, params=params)
        return response.json()

    def create_case(self, name: str, metadata: list = None) -> dict:
        """Creates a new case.

        The user provides their own case name, based on which Classy
        assigns and sends back a new internal id (case_id).

        name:
            An arbitrary case name as defined by the user.
        metadata (optional):
            Additional information provided by the user. Use the
            following format:
            [
                {"key": "content", "value": "content"},
                {"key": "content", "value": "content"},
            ]

        Returns:
            A new Searpent case id.
        """
        url = join_url(self.url, self._cases_url)
        data = {
            "name": name,
            "source": self.source,
        }
        if metadata is not None:
            data.update({"metadata": metadata})
        response = self.api.query("POST", url, data)
        return response.json()

    def update_case(
        self, case_id: str, name: str, correlation_id: str = None
    ) -> dict:
        """Updates the case name as displayed in the Classy interface.

        Args:
            case_id:
                A Searpent case id.
            name:
                A new case name.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.

        Returns:
            The case id and the updated case name.
        """
        url = join_url(self.url, self._cases_url, case_id)
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {"name": name, "correlation_id": correlation_id}
        response = self.api.query("PATCH", url, data)
        return response.json()

    def delete_case(
        self, case_id: str, correlation_id: str = None
    ) -> requests.Response:
        """Marks the case to be deleted after 3 days.

        Args:
            case_id:
                A Searpent case id.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.

        Returns:
            The response object can be used to verify the status code
            (response.status_code) which should equal to 200 for
            successful queries.
        """
        url = join_url(self.url, self._cases_url, case_id, "delete")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {"correlation_id": correlation_id}
        return self.api.query("POST", url, data=data)

    def cancel_delete_case(
        self, case_id: str, correlation_id: str = None
    ) -> requests.Response:
        """Cancels the case deletion.

        The "to be deleted" mark gets removed from the case.

        Args:
            case_id:
                A Searpent case id.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.

        Returns:
            The response object can be used to verify the status code
            (response.status_code) which should equal to 200 for
            successful queries.
        """
        url = join_url(self.url, self._cases_url, case_id, "cancel-delete")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {"correlation_id": correlation_id}
        return self.api.query("POST", url, data=data)

    def postpone_delete_case(self, case_id: str, ttl: str) -> dict:
        """
        Postpones the case deletion to a requested timepoint.

        Args:
            case_id:
                A Searpent case id.
            ttl:
                A requested deletion timepoint (ttl stands for "time-to-live")
                in the ISO8601 format, e.g. 2023-09-01T13:00:00.000Z (the actual
                deletion may take up to 48 hours though).

        Returns:
            The case id, its name and requested deletion timepoint.
        """
        url = join_url(self.url, self._cases_url, case_id)
        data = {"ttl": ttl}
        response = self.api.query("PATCH", url, data=data)
        return response.json()

    def upload_photo(
        self,
        case_id: str,
        photo_base64: bytes,
        filename: str,
        photo_id: str,
        correlation_id: str = None,
        metadata: list = None,
    ) -> dict:
        """Uploads a photo in base64 format to the case.

        Args:
            case_id:
                A Searpent case id.
            photo_base64:
                A photo represented as base64.
            filename:
                A photo filename.
            photo_id:
                An arbitrary photo name as defined by the user.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.
            metadata (optional):
                Additional information provided by the user. Use the
                following format:
                [
                    {"key": "content", "value": "content"},
                    {"key": "content", "value": "content"},
                ]

        Returns:
            A photo id assigned by the API.
        """
        url = join_url(self.url, self._cases_url, case_id, "/upload")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {
            "photo": photo_base64.decode(),
            "photo_id": photo_id,
            "filename": filename,
            "source": self.source,
            "correlation_id": correlation_id,
        }
        if metadata is not None:
            data.update({"metadata": metadata})

        response = self.api.query("PATCH", url, data)
        return response.json()

    def upload_photo_from_file(
        self,
        case_id: str,
        file_path: str,
        filename: str,
        photo_id: str,
        correlation_id: str = None,
        metadata: list = None,
    ) -> dict:
        """Uploads a photo file to the case.

        Args:
            case_id:
                A Searpent case id.
            file_path:
                A file path.
            filename:
                A photo filename.
            photo_id:
                An arbitrary photo name as defined by the user.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.
            metadata (optional):
                Additional information provided by the user. Use the
                following format:
                [
                    {"key": "content", "value": "content"},
                    {"key": "content", "value": "content"},
                ]

        Returns:
            A photo id assigned by the API.
        """
        url = join_url(self.url, self._cases_url, case_id, "/upload")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {
            "photo": convert_image(file_path),
            "photo_id": photo_id,
            "filename": filename,
            "source": self.source,
            "correlation_id": correlation_id,
        }
        if metadata is not None:
            data.update({"metadata": metadata})

        response = self.api.query("PATCH", url, data)
        return response.json()

    def upload_pdf(
        self,
        case_id: str,
        pdf_base64: bytes,
        filename: str,
        pdf_id: str,
        correlation_id: str = None,
        metadata: list = None,
    ) -> dict:
        """Uploads a PDF in base64 format to the case.

        Args:
            case_id:
                A Searpent case id.
            pdf_base64:
                A PDF represented as base64.
            filename:
                A PDF filename.
            pdf_id:
                An arbitrary PDF name as defined by the user.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.
            metadata (optional):
                Additional information provided by the user. Use the
                following format:
                [
                    {"key": "content", "value": "content"},
                    {"key": "content", "value": "content"},
                ]

        Returns:
            A PDF id assigned by the API.
        """
        if Path(filename).suffix != ".pdf":
            raise ValueError("Filename must end with .pdf extension")

        url = join_url(self.url, self._cases_url, case_id, "/pdf/upload")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {
            "photo": pdf_base64.decode(),
            "photo_id": pdf_id,
            "filename": filename,
            "source": self.source,
            "correlation_id": correlation_id,
        }
        if metadata is not None:
            data.update({"metadata": metadata})

        response = self.api.query("PATCH", url, data)
        return response.json()

    def upload_pdf_from_file(
        self,
        case_id: str,
        file_path: str,
        filename: str,
        pdf_id: str,
        correlation_id: str = None,
        metadata: list = None,
    ) -> dict:
        """Uploads a PDF file to the case.

        Args:
            case_id:
                A Searpent case id.
            file_path:
                A file path.
            filename:
                A PDF filename.
            pdf_id:
                An arbitrary PDF name as defined by the user.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.
            metadata (optional):
                Additional information provided by the user. Use the
                following format:
                [
                    {"key": "content", "value": "content"},
                    {"key": "content", "value": "content"},
                ]

        Returns:
            A PDF id assigned by the API.
        """
        if Path(file_path).suffix != ".pdf" or Path(filename).suffix != ".pdf":
            raise ValueError(
                "File path and filename must both end with .pdf extension"
            )

        url = join_url(self.url, self._cases_url, case_id, "/pdf/upload")
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {
            "photo": convert_image(file_path),
            "photo_id": pdf_id,
            "filename": filename,
            "source": self.source,
            "correlation_id": correlation_id,
        }
        if metadata is not None:
            data.update({"metadata": metadata})

        response = self.api.query("PATCH", url, data)
        return response.json()

    def list_exports(
        self, exp_type: str, from_time: str = None, to_time: str = None
    ) -> list:
        """Retrieves a list of performed exports.

        There are two types of exports to pick from:
        'regular' or 'custom'.

        If from_time and to_time are not specified, only inspections
        which have less than 90 days will be returned if available.
        An empty array will be returned otherwise.

        Args:
            exp_type:
                The export type with 'regular' or 'custom' value.
            from_time (optional):
                Start time, e.g. '2021-09-01T13:00:00.000Z'.
            to_time (optional):
                End time, e.g. '2021-09-01T15:00:00.000Z'.

        Returns:
            A list of exports performed by the user.
        """
        from_time = (
            None if from_time is None else validate_iso_datetime(from_time)
        )
        to_time = None if to_time is None else validate_iso_datetime(to_time)
        url = join_url(self.url, self._exports_url)
        params = {
            "from": from_time,
            "to": to_time,
            "source": self.source,
            "type": exp_type,
        }
        response = self.api.query("GET", url, params=params)
        return response.json()

    def get_export(self, exp_id: str) -> dict:
        """Retrieves one particular export.

        Args:
            exp_id:
                The export id.

        Returns:
            Metadata related to the export.
        """
        url = join_url(self.url, self._exports_url, exp_id)
        response = self.api.query("GET", url)
        return response.json()

    def get_export_csv(self, exp_id: str, file_path: str = None) -> None:
        """Retrieves a csv file with requested export.

        Args:
            exp_id:
                The export id.
            file_path (optional):
                A file path to store the result.
        """
        response = self.api.query(
            "GET", join_url(self.url, self._exports_url, exp_id, "/download")
        )
        default_name = f"searpent-classy-{self.source}-{exp_id}.csv"
        path = default_name if file_path is None else file_path

        with open(path, "w", encoding="utf-8") as file:
            file.write(response.text)

    def get_export_download_url(self, exp_id: str) -> str:
        """Retrieves a csv download url for the requested export.

        Args:
            exp_id:
                The export id.

        Returns:
            A csv download url.
        """
        url = join_url(self.url, self._exports_url, exp_id)
        response = self.api.query("GET", url)
        content = response.json()
        return content.get("url")

    def list_inspections(
        self, from_time: str = None, to_time: str = None
    ) -> list:
        """Retrieves a list of performed inspections.

        If from_time and to_time not specified, inspections
        no older than 90 days will be returned if available,
        an empty array otherwise.

        Args:
            from_time (optional):
                Start time, e.g. '2021-09-01T15:00:00.000Z'.
            to_time (optional):
                End time, e.g. '2021-09-01T15:00:00.000Z'.

        Returns:
            A list of inspections performed by the user.
        """
        from_time = (
            None if from_time is None else validate_iso_datetime(from_time)
        )
        to_time = None if to_time is None else validate_iso_datetime(to_time)
        url = join_url(self.url, self._inspections_url)
        params = {"from": from_time, "to": to_time, "source": self.source}
        response = self.api.query("GET", url, params=params)
        return response.json()

    def get_inspection(self, inspection_id: str) -> dict:
        """Retrieves one particular inspection.

        Atrs:
            inspection_id:
                A Searpent inspection id.

        Returns:
            Metadata related to the inspection.
        """
        url = join_url(self.url, self._inspections_url, inspection_id)
        response = self.api.query("GET", url)
        return response.json()

    def get_inspection_with_photos(self, inspection_id: str) -> dict:
        """Retrieves one particular inspection with attached photos.

        Atrs:
            inspection_id:
                A Searpent inspection id.

        Returns:
            Metadata related to the inspection.
        """
        url = join_url(self.url, self._inspections_url, inspection_id)
        params = {"withPhotos": "true"}
        response = self.api.query("GET", url, params=params)
        return response.json()

    def create_inspection(
        self,
        name: str,
        required_fields: List[Dict[str, str]],
        phone: str = None,
        message: str = None,
        send_at: str = None,
        metadata: list = None,
    ) -> dict:
        """Creates a new inspection.

        Args:
            name:
                An insuser inspection name.
            required_fields:
                One or multiple fields specific to the insurer in a form
                of a list of dictionaries. It has to contain the
                "fieldId" and "requiredText" keys as presented below:
                [
                    {
                    "fieldId": "policy number",
                    "requiredText": "c-0001"
                    },
                    {
                    "fieldId": "surname",
                    "requiredText": "doe"
                    }
                ]
            phone (optional):
                A phone number of the recipient. If the phone number
                is defined, an SMS will be automatically sent to it.
                Consult https://www.twilio.com/docs/glossary/what-e164
                for required formats.
            message (optional):
                An invitation message sent to the recipient, it has
                to include the '%s' string that will be replaced
                with an inspection url, e.g. "Please click on %s
                to start inspection".
            send_at (optional):
                An SMS dispatch time. It must be set in the ISO8601 format,
                e.g. 2021-09-01T13:00:00.000Z, and must be greater than
                the current time by at least 1h.
            metadata (optional):
                Additional information provided by the user. Use the
                following format:
                [
                    {"key": "content", "value": "content"},
                    {"key": "content", "value": "content"},
                ]

        Returns:
            An inspection.
        """
        if send_at and not phone:
            raise ValueError(
                "If the send_at argument is defined, the phone"
                " argument must also be supplied"
            )

        url = join_url(self.url, self._inspections_url)
        data = {
            "name": name,
            "source": self.source,
            "requiredFields": required_fields,
        }

        if phone is not None:
            data.update({"phone": phone})
        if message is not None:
            if "%s" not in message:
                raise ValueError(
                    "'%s' tag not found in the invitation message"
                )
            data.update({"invitationMessage": message})
        if send_at is not None:
            send_at = validate_iso_datetime(send_at)
            data.update({"sendAt": send_at})
        if metadata is not None:
            data.update({"metadata": metadata})

        response = self.api.query("POST", url, data)
        return response.json()

    def delete_inspection(
        self,
        inspection_id: str,
        correlation_id: str = None,
    ) -> requests.Response:
        """Marks the inspection to be deleted after 3 days.

        Args:
            inspection_id:
                A Searpent inspection id.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.

        Returns:
            The response object can be used to verify the status code
            (response.status_code) which should equal to 200 for
            successful queries.
        """
        url = join_url(
            self.url, self._inspections_url, inspection_id, "delete"
        )
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {"correlation_id": correlation_id}
        return self.api.query("POST", url, data=data)

    def cancel_delete_inspection(
        self,
        inspection_id: str,
        correlation_id: str = None,
    ) -> requests.Response:
        """Cancels the inspection deletion.

        The "to be deleted" mark gets removed from the inspection.

        Args:
            inspection_id:
                A Searpent inspection id.
            correlation_id (optional):
                An id set to track the request. If not provided
                by the user, an uuid is generated automatically.

        Returns:
            The response object can be used to verify the status code
            (response.status_code) which should equal to 200 for
            successful queries.
        """
        url = join_url(
            self.url, self._inspections_url, inspection_id, "cancel-delete"
        )
        correlation_id = (
            str(uuid.uuid4()) if not correlation_id else correlation_id
        )
        data = {"correlation_id": correlation_id}
        return self.api.query("POST", url, data=data)

    def postpone_delete_inspection(self, inspection_id: str, ttl: str) -> dict:
        """
        Postpones the inspection deletion to a requested timepoint.

        Args:
            inspection_id:
                A Searpent inspection id.
            ttl:
                A requested deletion timepoint (ttl stands for "time-to-live")
                in the ISO8601 format, e.g. 2023-09-01T13:00:00.000Z.

        Returns:
            The inspection id, its name and requested deletion timepoint.
        """
        url = join_url(self.url, self._inspections_url, inspection_id)
        ttl = validate_iso_datetime(ttl)
        data = {"ttl": ttl}
        response = self.api.query("PATCH", url, data=data)
        return response.json()
