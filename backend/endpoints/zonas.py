from fastapi import APIRouter
from db import get_connection
import json
from pathlib import Path

router = APIRouter()  

@router.get("/api/zonas-con-datos")
def zonas_geojson():
    conn = get_connection()
    cursor = conn.cursor()

    # Agrupamos los datos por zona
    cursor.execute("""
        SELECT Zona,
               SUM(PoblacionTotal) AS PoblacionTotal,
               SUM(Varones) AS Varones,
               SUM(Mujeres) AS Mujeres,
               SUM(Hogares) AS Hogares,
               SUM(HogaresNBI) AS HogaresNBI,
               SUM(PoblacionSinCobertura) AS PoblacionSinCobertura
        FROM Vista_2022AreasProgramaticas
        GROUP BY Zona
    """)
    
    # Creamos el dict {zona: fila}
    datos = {row.Zona: row for row in cursor.fetchall()}
    print(f"✅ Zonas agrupadas desde SQL: {len(datos)}")

    with open(Path("geojson_base/ZONA.json"), encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson["features"]:
        nombre = feature["properties"].get("name", "")
        zona_id_str = nombre.replace("ZONA ", "").strip()
        zona_id = int(zona_id_str) if zona_id_str.isdigit() else None

        if zona_id and zona_id in datos:
            row = datos[zona_id]
            feature["properties"].update({
                "poblacion": row.PoblacionTotal,
                "mujeres": row.Mujeres,
                "varones": row.Varones,
                "hogares": row.Hogares,
                "hogares_nbi": row.HogaresNBI,
                "cobertura": row.PoblacionSinCobertura
            })
            print(f"✅ ZONA {zona_id} actualizada: {row.PoblacionTotal} habs")
        else:
            print(f"❌ No se encontró data para zona_id={zona_id} ({nombre})")

    return geojson


