from fastapi import APIRouter
from db import get_connection

router = APIRouter()

@router.get("/api/efectores")
def efectores():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Seleccionamos solo los distintos Centros de Salud, usando MIN para evitar duplicados
        cursor.execute("""
            SELECT Centro,
                   MIN(Latitud) AS Latitud,
                   MIN(Longitud) AS Longitud,
                   MIN(Institucion) AS Institucion,
                   MIN(Tipo) AS Tipo,
                   MIN(Direccion) AS Direccion,
                   MIN(Horario) AS Horario,
                   MIN(a.Zona) AS Zona
            FROM Vista_CentrosHorarios v
            LEFT JOIN Vista_2022AreasProgramaticas a ON v.Id = a.Id
            WHERE v.Tipo = 'Centro de Salud'
            GROUP BY Centro
        """)

        features = []
        for row in cursor.fetchall():
            if row.Latitud is None or row.Longitud is None:
                continue

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row.Longitud), float(row.Latitud)]
                },
                "properties": {
                    "centro": row.Centro,
                    "institucion": row.Institucion,
                    "tipo": row.Tipo,
                    "direccion": row.Direccion,
                    "horario": row.Horario,
                    "zona": row.Zona
                }
            })

        return {"type": "FeatureCollection", "features": features}
    except Exception as e:
        return {"error": str(e)}

