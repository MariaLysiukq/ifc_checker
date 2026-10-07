import uuid
import zipfile
from datetime import datetime
from textwrap import dedent

from ifc_checker.core.interfaces import IReporter
from ifc_checker.core.models import ValidationResult


class BcfReporter(IReporter):
    """Generates a BCF 2.1 compliant .bcfzip file for direct BIM software integration."""

    def generate(self, result: ValidationResult, output_path: str) -> None:
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if not output_path.lower().endswith(".bcfzip"):
            output_path += ".bcfzip"

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as bcf_zip:
            bcf_zip.writestr("bcf.version", "2.1")
            for issue in result.issues:
                topic_guid = str(uuid.uuid4())
                severity_map = {"CRITICAL": "Error", "ERROR": "Error", "WARNING": "Warning"}
                bcf_severity = severity_map.get(issue.severity.name, "Info")
                markup_content = dedent(
                    f"""\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <Markup>
                      <Topic Guid="{topic_guid}" TopicType="{bcf_severity}" TopicStatus="Open">
                        <Title>[{issue.rule_id}] {issue.element_type} Compliance Issue</Title>
                        <CreationDate>{timestamp}</CreationDate>
                        <CreationAuthor>ifc-checker</CreationAuthor>
                      </Topic>
                      <Comment>
                        <Date>{timestamp}</Date>
                        <Author>ifc-checker</Author>
                        <Comment><![CDATA[{issue.message}]]></Comment>
                        <Viewpoint>
                          <Viewpoint>viewpoint.bcfv</Viewpoint>
                        </Viewpoint>
                      </Comment>
                    </Markup>
                """
                )

                viewpoint_content = dedent(
                    f"""\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <VisualizationInfo>
                      <Components>
                        <Selection>
                          <Component IfcGuid="{issue.element_id}" />
                        </Selection>
                      </Components>
                    </VisualizationInfo>
                """
                )

                bcf_zip.writestr(f"{topic_guid}/markup.bcf", markup_content)
                bcf_zip.writestr(f"{topic_guid}/viewpoint.bcfv", viewpoint_content)
