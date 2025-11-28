import oci
import os
import subprocess
import json

def handler(ctx, data: io.BytesIO = None):
    oac_ocid = "ocid1.analyticsinstance.oc1.ap-tokyo-1.aaaaaaaaurpers4kla3u4mo7c3pz35elstyvrdhhev5wwmwmx77rekwr25pq"
    if not oac_ocid:
        return {"status": "FAILED", "message": "OAC_INSTANCE_OCID environment variable is missing."}

    # 停止コマンドの実行
    cli_command = [
        "oci", "analytics", "analytics-instance", "stop", # stopコマンドを使用
        "--analytics-instance-id", oac_ocid,
        "--wait-for-state", "SUCCEEDED"
    ]

    try:
        result = subprocess.run(cli_command, capture_output=True, text=True, check=True)
        return {"status": "SUCCEEDED", "message": "OAC instance stopped successfully.", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "FAILED", "message": f"CLI command failed: {e.stderr}", "error_code": e.returncode}
    except Exception as e:
        return {"status": "ERROR", "message": f"An unexpected error occurred: {str(e)}"}
