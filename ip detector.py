import re
from collections import defaultdict

def analizar_log(contenido_log):
    
    codigos_fallo = ['401', '403', '404', '500']
    conteo_fallos = defaultdict(int)
    detalle_ip = defaultdict(list)
    
    patron_acceso = r'(\d+\.\d+\.\d+\.\d+|x\.x\.x\.\d+).*?"(\w+)\s+(\S+).*?"\s+(\d{3})'
    patron_error = r'\[client\s+(\d+\.\d+\.\d+\.\d+)\]'
    
    for linea in contenido_log.strip().split('\n'):
        
        match_acceso = re.search(patron_acceso, linea)
        if match_acceso:
            ip = match_acceso.group(1)
            metodo = match_acceso.group(2)
            ruta = match_acceso.group(3)
            codigo = match_acceso.group(4)
            
            if codigo in codigos_fallo:
                conteo_fallos[ip] += 1
                detalle_ip[ip].append(f"{codigo} {metodo} {ruta}")
        
        match_error = re.search(patron_error, linea)
        if match_error:
            ip = match_error.group(1)
            conteo_fallos[ip] += 1
            detalle_ip[ip].append(f"ERROR: {linea.strip()[-60:]}")
    
    print("=" * 60)
    print("REPORTE DE ANÁLISIS SOC — LOG APACHE")
    print("=" * 60)
    
    print("\n[TODAS LAS IPs CON ACTIVIDAD FALLIDA]")
    for ip, total in sorted(conteo_fallos.items(), 
                            key=lambda x: x[1], reverse=True):
        nivel = "🔴 CRÍTICO" if total >= 5 else "🟡 SOSPECHOSO" if total >= 2 else "🟢 REVISAR"
        print(f"\n{nivel} | IP: {ip} | Fallos: {total}")
        for evento in detalle_ip[ip][:5]:
            print(f"   → {evento}")
        if len(detalle_ip[ip]) > 5:
            print(f"   → ... y {len(detalle_ip[ip])-5} eventos más")
    
    print("\n[IPs CON MÁS DE 10 PETICIONES FALLIDAS]")
    criticas = {ip: t for ip, t in conteo_fallos.items() if t > 10}
    if criticas:
        for ip, total in criticas.items():
            print(f"⛔ ALERTA: {ip} — {total} fallos detectados")
    else:
        print("Ninguna IP supera el umbral de 10 en este log.")
        print("IP más activa:", max(conteo_fallos, key=conteo_fallos.get),
              "con", max(conteo_fallos.values()), "fallos")

log = """192.168.2.20 - - [28/Jul/2006:10:27:10 -0300] "GET /cgi-bin/try/ HTTP/1.0" 200 3395
127.0.0.1 - - [28/Jul/2006:10:22:04 -0300] "GET / HTTP/1.0" 200 2216
x.x.x.90 - - [13/Sep/2006:07:01:53 -0700] "PROPFIND /svn/[xxxx]/Extranet/branches/SOW-101 HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:07:01:51 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/trunk HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:07:00:53 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/2.5 HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:07:00:53 -0700] "PROPFIND /svn/[xxxx]/Extranet/branches/SOW-101 HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:07:00:21 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/trunk HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:06:59:53 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/2.5 HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:06:59:50 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/trunk HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:06:58:52 -0700] "PROPFIND /svn/[xxxx]/[xxxx]/trunk HTTP/1.1" 401 587
x.x.x.90 - - [13/Sep/2006:06:58:52 -0700] "PROPFIND /svn/[xxxx]/Extranet/branches/SOW-101 HTTP/1.1" 401 587
127.0.0.1 - - [28/Jul/2006:10:27:32 -0300] "GET /hidden/ HTTP/1.0" 404 7218
[Fri Dec 16 01:46:23 2005] [error] [client 1.2.3.4] Directory index forbidden by rule: /home/test/
[Fri Dec 16 01:54:34 2005] [error] [client 1.2.3.4] Directory index forbidden by rule: /apache/web-data/test2
[Fri Dec 16 02:25:55 2005] [error] [client 1.2.3.4] Client sent malformed Host header
[Mon Dec 19 23:02:01 2005] [error] [client 1.2.3.4] user test: authentication failure for "/~dcid/test1": Password Mismatch"""

analizar_log(log)
