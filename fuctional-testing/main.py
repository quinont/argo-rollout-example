import subprocess
import os
from git import Repo


def clone_repo(repo_url, commit_hash):
    """
    Clonea un repo de git en un commit especial.

    Args:
        repo_url: La URL del repo de git.
        commit_hash: El hash del commit especial.

    Returns:
        El directorio del repo clonado.
    """
    repo_dir = os.path.join(".", os.path.basename(repo_url))
    if os.path.exists(repo_dir):
        subprocess.run(["rm", "-rf", repo_dir])
    try:
        repo = Repo.clone_from(repo_url, 'argo-rollout-example')

        # Cambiar al commit específico
        repo.git.reset('--hard', commit_hash)

        print("Clonado y restablecido con éxito.")
    except Exception as e:
        raise Exception(f"Error al clonar o restablecer el repositorio: {e}")
    return repo_dir


def install_requirements(repo_dir, folder):
    """
    Instala las dependencias necesarias para correr los tests

    Args:
        repo_dir: El directorio del repo.
        folder: El directorio donde estan las pruebas

    Returns:
        El exit code del pip install
    """
    path_to_requirements = os.path.join(repo_dir, folder, "requirements.txt")
    if os.path.isfile(path_to_requirements):
        print("Se encontro un archivo requirements.txt, instalando")
        return subprocess.call(["pip3", "install", "-r", path_to_requirements])

    print("No se encontro un archivo requirements.txt")
    return 0


def run_tests(repo_dir, folder):
    """
    Ejecuta los test unitarios de un repo.

    Args:
        repo_dir: El directorio del repo.
        folder: El directorio donde estan las pruebas

    Returns:
        El exit code de los test.
    """
    test_files = []
    for f in os.listdir(os.path.join(repo_dir, folder)):
        if os.path.isfile(os.path.join(repo_dir, folder, f)):
            if f.endswith(".py"):
                test_files.append(os.path.join(repo_dir, folder, f))
    print(f"Archivos encontrados: {test_files}")
    return subprocess.call(["pytest", *test_files])


if __name__ == "__main__":
    repo_url = os.getenv("REPO_URL")
    if repo_url is None:
        raise Exception("No se encontro variable de entorno REPO_URL")

    commit_hash = os.getenv("COMMIT_HASH")
    if commit_hash is None:
        raise Exception("No se encontro variable de entorno COMMIT_HASH")

    folder_test = os.getenv("FOLDER_TEST")
    if folder_test is None:
        raise Exception("No se encontro variable de entorno FOLDER_TEST")

    repo_dir_clone = clone_repo(repo_url, commit_hash)
    exit_code_install = install_requirements(repo_dir_clone, folder_test)
    if exit_code_install != 0:
        raise Exception("No se pudo instalar los requirements para los test.")

    exit_code = run_tests(repo_dir_clone, folder_test)
    if exit_code != 0:
        raise Exception("Los test fallaron.")
