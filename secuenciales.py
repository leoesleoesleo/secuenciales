#!/usr/bin/env python3

# Standar Library
import random
import json
import subprocess

# Internal Library
from settings import logger


def load_file_json(ruta):
  try:
    with open(ruta, 'r') as archivo:
      datos = json.load(archivo)
      return datos
  except FileNotFoundError:
    logger.warning(f"El archivo '{ruta}' no se encontró.")
  except json.JSONDecodeError:
    logger.error(
        f"Error al decodificar el JSON en '{ruta}'. Asegúrate de que el archivo JSON sea válido."
    )
  return None


def execute_job(job):
  if job["last_run"] == "error":
    return False
  else:
    logger.info(
        f"EJECUTANDO EL JOB: {job['name_job']} PRIORIDAD: {job['priority']}")

    command = "ls -l"
    resultado, retorno = run_command_in_shell(command=command,
                                              name_job=job['name_job'])
    print(f"Resultado:\n{resultado}")
    print(f"Código de retorno: {retorno}")

    logger.info(
        f"  -> TERMINADO EL JOB: {job['name_job']} PRIORIDAD: {job['priority']}"
    )
    return True


def run_command_in_shell(*, command: str, name_job: str):
  try:
    # Ejecuta el comando y captura la salida estándar y el código de retorno
    response = subprocess.check_output(command,
                                       shell=True,
                                       stderr=subprocess.STDOUT,
                                       text=True)
    return_code = 0
  except subprocess.CalledProcessError as e:
    logger.error(f"Al llamar el JOB {name_job} con el comando {e}")
    response = e.output
    return_code = e.returncode

  return response, return_code
