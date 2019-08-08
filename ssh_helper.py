import paramiko,time


class SshHelper:

    """
    SSH Helper class to connect with remote server for command execution , file transfer and all
    """

    def __init__(self, username, password, host, port=22):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        """
        connect to remote server using PASSWORD less or PASSWORD based
        authentication
        """
        conn = None
        try:
            if self.host and self.username and self.password and self.password.strip():
                conn = paramiko.SSHClient()
                conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                conn.connect(hostname=self.host, username=self.username,
                             password=self.password.strip(), port=self.port)
            else:
                print("Unable to connect to remote server; not enough info was given.")
        except Exception as err:
            print("Error in Connecting to the host.. {0}".format(err))
        return conn

    def connect_to_host(self,retry_count=3):
        """
        Connect to remote host and return connection object
        default retry count is 3
        """
        retry_count, count = retry_count, retry_count
        while True:
            try:
                conn = self.connect()
                break
            except Exception:
                retry_count -= 1
                if retry_count < 0:
                    print("Unable to Connect to Host %s ,Even after %s Retries ",self.host, count)
                    raise Exception('Unable to Connect to the Host {0} after several retries'.format(self.host))
                time.sleep(10)
        return conn

    def connect_to_exec_command(self, command, print_cmd=True):
        """
        Connect to ssh client and invoke exec_command for command execution and get
        the exit status,if command execution is not successful then raise exception
        :param command - command to execute
        :param print_cmd - print cmd on log file
        :raise : VOSSException -if command execution fails
        """
        if print_cmd:
            print ("Connect to '%s' to Execute Command :%s", self.host, command)
        connected = False
        conn = None
        try:
            conn = self.connect_to_host()
            connected = True
            self.exec_command(conn, command)
        except Exception as err:
            print(err.message)
            raise Exception(err)
        finally:
            if connected is True and conn is not None:
                self.disconnect(conn)
        print ("Command Execution Completed")

    def exec_command(self, conn, command):
        """
        Execute a command on the SSH server. The command's output and error
        streams are returned to stdout, and stderr. command exit status is
        returned to exit_status. '0' for successful execution
        :param conn - connection object
        :param str command: the command to execute
        :return exit_status : to indicate the command execution status
        """
        try:
            std_in, std_out, std_err = conn.exec_command(command)
            for line in std_out.readlines():
                print (line.strip('\n'))
            exit_status = std_out.channel.recv_exit_status()
            if exit_status != 0:
                for line in std_err.readlines():
                    print (line.strip('\n'))
                if std_in:
                    print ("Command Execution is not Successful")
                raise Exception()
            print ("Command Executed Successfully on '%s' ", self.host)
        except Exception as err:
            print (err)
            raise Exception("Error in Connecting to host")

    def exec_command_forward_output(self, command):
        """
        Connect to  ssh client and invoke exec_command for command execution and get
        the exit status, stdout,stderr and forward it to caller
        :param command - command to execute
        :param print_cmd - print cmd on log file
        :raise : Exceptions -if command execution fails
        """
        std_out, std_err, exit_status = '','', 1
        connected = False
        conn = None
        try:
            conn = self.connect_to_host()
            std_in, std_out, std_err = conn.exec_command(command)
            exit_status = std_out.channel.recv_exit_status()
            if exit_status == 0 and std_in:
                print ("Execute Command and Redirect std info %s ", command)
        except Exception as err:
            print(err.message)
        finally:
            if connected is True and conn is not None:
                self.disconnect(conn)
        print ("Command has been executed successfully. ")
        for out in std_out:
            print out
        for err in std_err:
            print err
        return std_out, std_err, exit_status

    def disconnect(self, conn):
        """
        Close this SSHClient.
        :param close conn object
        """
        print ("Close Connection for Host {0}".format(self.host))
        if conn:
            conn.close()

if False and __name__ == "__main__":

    ssh = SshHelper(username='user', password='pswd', host='X.X.X.X')
    conn = ssh.connect_to_host()
    ssh_stdin, ssh_stdout, ssh_stderr = conn.exec_command("ls -larth")
    exit_status = ssh_stdout.channel.recv_exit_status()
    print exit_status
    print ssh_stdout.read()
