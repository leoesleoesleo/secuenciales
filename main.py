#!/usr/bin/env python3

# Standar Library
from datetime import datetime
import concurrent.futures

# Internal Library
from settings import logger
from secuenciales import load_file_json, execute_job

start_time = datetime.now()
logger.info(f"***************NUEVA EJECUCION: {start_time} ***************")

JSON_JOBS = load_file_json("secuencial.json")
"""Agrupa los trabajos por prioridad"""
priority_jobs = {}

for job in JSON_JOBS:
  priority = job["priority"]
  if priority not in priority_jobs:
    priority_jobs[priority] = []

  priority_jobs[priority].append(job)
"""Ordena las prioridades de menor a mayor"""
sorted_priorities = sorted(priority_jobs.keys())
"""Ejecuta los trabajos secuencialmente y los de la misma prioridad en paralelo"""
error_occurred = False

with concurrent.futures.ThreadPoolExecutor() as executor:
  for priority in sorted_priorities:
    jobs = priority_jobs[priority]
    if len(jobs) == 1:
      # Si solo hay un trabajo, ejecútalo secuencialmente
      response = execute_job(jobs[0])
      if not response:
        logger.error(
            f"El JOB {jobs[0]['name_job']} no se ejecutó correctamente:: *FIN DEL PROGRAMA*"
        )
        error_occurred = True
        break
    else:
      # Si hay varios trabajos con la misma prioridad, ejecútalos en paralelo
      futures = [executor.submit(execute_job, job) for job in jobs]
      # Espera a que todos los trabajos de la misma prioridad se completen
      concurrent.futures.wait(futures)
      # Verifica los resultados de los trabajos en paralelo
      for future in futures:
        result = future.result()
        if not result:
          # Realiza acciones específicas si el resultado es False para trabajos paralelos
          for job_ in jobs:
            if job_["last_run"] == "error":
              logger.error(
                  f"El JOB {job_['name_job']} no se ejecutó correctamente:: *FIN DEL PROGRAMA*"
              )
              error_occurred = True
              break  # Sal del bucle externo si hay un error
          break
      if error_occurred:
        break  # Sal del bucle externo si hay un error
