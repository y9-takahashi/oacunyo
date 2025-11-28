import oci
import os
import subprocess
import json

def handler(ctx, data: io.BytesIO = None):
    # 環境変数からOACインスタンスのOCIDを取得
    oac_ocid = os.environ.get("OAC_INSTANCE_OCID")
    if not oac_ocid:
        return {"status": "FAILED", "message": "OAC_INSTANCE_OCID environment variable is missing."}

    # 起動コマンドの実行
    # OCI CLIは、ファンクション環境でリソース・プリンシパルを使用して認証されます。
    cli_command = [
        "oci", "analytics", "analytics-instance", "start",
        "--analytics-instance-id", oac_ocid,
        "--wait-for-state", "SUCCEEDED"
    ]

    try:
        result = subprocess.run(cli_command, capture_output=True, text=True, check=True)
        return {"status": "SUCCEEDED", "message": "OAC instance started successfully.", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "FAILED", "message": f"CLI command failed: {e.stderr}", "error_code": e.returncode}
    except Exception as e:
        return {"status": "ERROR", "message": f"An unexpected error occurred: {str(e)}"}
