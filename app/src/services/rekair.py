from src.models.rekair_model import RekairModel
from src.schema.rekair_schm import RekairSchema
from ..core.db import get_raw_database_session
import pandas as pd
from sqlalchemy.orm import Session


def getRekair(periode):
    connection = get_raw_database_session()
    with connection:
        with connection.cursor() as cursor:
            sql = """
                    SELECT
                        nosamw,
                        alamat,
                        periode,
                        met_l,
                        met_k,
                        pakai,
                        dnmet,
                        r1,
                        r2,
                        r3,
                        r4,
                        denda,
                        ang_sb,
                        jasa_sb
                    FROM
                        rekair
                    WHERE
                        periode = %s
                """
            cursor.execute(sql, (periode,))
            rows = cursor.fetchall()
            cursor.close()
            return rows


def get_rekening_tni(periode: str) -> pd.DataFrame:
    connection = get_raw_database_session()
    with connection:
        with connection.cursor() as cursor:
            sql = """
                    SELECT
                        'PDAM Kabupaten Banyumas' AS pdam,
                        m.kotama AS matra,
                        m.satker,
                        r.nosamw,
                        m.nama,
                        r.alamat,
                        r.periode,
                        r.met_l,
                        r.met_l as met_l_ori,
                        r.met_k,
                        r.met_k as met_k_ori,
                        r.pakai,
                        r.pakai as pakai_ori,
                        r.rata2,
                        r.rata2 as rata2_ori,
                        r.dnmet,
                        r.r1,
                        r.r2,
                        r.r3,
                        r.r4,
                        r.t1,
                        r.t2,
                        r.t3,
                        r.t4,
                        r.denda,
                        r.ang_sb,
                        r.jasa_sb
                    FROM
                        rekair r
                    INNER JOIN master_tni m ON r.nosamw = m.nosamw
                    WHERE
                        r.periode = %s
                """
            cursor.execute(sql, (periode,))
            data = cursor.fetchall()
            if len(data) == 0: return None
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            cursor.close()
            return df


def detail_rekening(nosamw: str, periode: str, db: Session) -> RekairSchema | None:
    stmt = db.query(RekairModel).filter(
        RekairModel.nosamw == nosamw,
        RekairModel.periode == periode,
        RekairModel.statrek == "A"
    )
    # print(stmt)
    result: RekairModel | None = stmt.first()
    return result
