import paramiko
from config.settings import HOSTNAME

class SSHClient:
    def __init__(self):
        self._client = None
        self.hostname = HOSTNAME

    def get_node_info(self, username=None, password=None):
        """Fetches node information using SSH and returns the output as a string."""
        try:
            if not self._client or not username:
                self._connect(username, password)

            stdin, stdout, stderr = self._client.exec_command("scontrol show node")
            output = stdout.read().decode()
            return output
        except Exception as e:
            print(f"An error occurred while fetching node info: {e}")
            return None
        finally:
            if self._client:
                self._client.close()
                self._client = None

    def test_connection(self, username: str, password: str) -> bool:
        """Test SSH connection with provided credentials."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=username, password=password)
            ssh.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except Exception as e:
            print(f"SSH connection test error: {e}")
            return False

    def _connect(self, username: str, password: str):
        """Establish SSH connection."""
        if not self._client:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(self.hostname, username=username, password=password)