import os
import platform
import subprocess






def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


class Build():
    def server(version):
        pip = os.path.realpath(os.path.join(os.getcwd(), "./Server/env/Scripts/pip.exe"))
        nuitka = os.path.realpath(os.path.join(os.getcwd(), "./Server/env/Scripts/nuitka.bat"))
        server_py = os.path.realpath(os.path.join(os.getcwd(), "./Server/Server.py"))
        ico = os.path.realpath(os.path.join(os.getcwd(), "./Server/static/icon.ico"))
        process = subprocess.Popen(f"\"{pip}\" install nuitka", shell=True)
        process.wait()
        args = [
            nuitka,
            server_py,
            "--include-package=sentry_sdk",
            "-o Chat Server.exe",
            "--remove-output",
            "--standalone",
            "--onefile",
            "--company-name=Serpent Modding",
            "--product-name=Chat Server",
            f"--file-version={version}",
            "--file-description=A simple server for Serpent Modding's Chat Client",
            f"--windows-icon-from-ico={ico}"]
        process = subprocess.Popen(args, shell=True)
        process.wait()
        process = subprocess.Popen(f"\"{pip}\" uninstall nuitka ordered-set zstandard -y", shell=True)
        process.wait()
        
    
    def client(version):
        pip = os.path.realpath(os.path.join(os.getcwd(), "./Client/env/Scripts/pip.exe"))
        nuitka = os.path.realpath(os.path.join(os.getcwd(), "./Client/env/Scripts/nuitka.bat"))
        client_py = os.path.realpath(os.path.join(os.getcwd(), "./Client/Client.py"))
        static = os.path.realpath(os.path.join(os.getcwd(), "./Client/static"))
        ico = os.path.join(static, "icon.ico")
        process = subprocess.Popen(f"\"{pip}\" install nuitka", shell=True)
        process.wait()
        args = [
            nuitka,
            client_py,
            "--plugin-enable=tk-inter",
            "-o Chat Client.exe",
            "--remove-output",
            "--standalone",
            #"--onefile",
            "--disable-console",
            "--company-name=Serpent Modding",
            "--product-name=Chat Client",
            f"--file-version={version}",
            f"--include-data-dir={static}=static",
            "--file-description=A simple client for Serpent Modding's Chat Server",
            f"--windows-icon-from-ico={ico}"]
        process = subprocess.Popen(args, shell=True)
        process.wait()
        process = subprocess.Popen(f"\"{pip}\" uninstall nuitka ordered-set zstandard -y", shell=True)
        process.wait()
    
    
    def docker():
        def find_executable(executable):
            for path in os.environ["PATH"].split(os.pathsep):
                exe_path = os.path.join(path, executable)
                if os.path.exists(exe_path) and os.access(exe_path, os.X_OK):
                    return exe_path
            return None
        docker = find_executable("docker.exe")
        process = subprocess.Popen(f"\"{docker}\" build -t serpensin/chatserver:latest ./Server", shell=True)
        process.wait()


def make_selection():
    clear()
    selection = input("Build Server, Client, Both, or Docker Image? [S/C/B/D]: ")
    if selection.lower() == "s":
        server_version = input("Enter Server Version: ")
        clear()
        Build.server(server_version)
    elif selection.lower() == "c":
        client_version = input("Enter Client Version: ")
        clear()
        Build.client(client_version)
    elif selection.lower() == "b":
        server_version = input("Enter Server Version: ")
        client_version = input("Enter Client Version: ")
        clear()
        Build.server(server_version)
        Build.client(client_version)
    elif selection.lower() == "d":
        clear()
        Build.docker()
    else:
        make_selection()





if __name__ == "__main__":
    make_selection()

