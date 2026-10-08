from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.dependencies import require_roles
from app.database import get_db
from app.models import Frequentation, User


router = APIRouter(prefix="/analytics", tags=["Securisé"])


@router.get("/bilan")
def get_bilan(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("analyst")),
):
    stmt = select(
        func.count(Frequentation.id).label("nb_observations"),
        func.sum(Frequentation.visiteurs).label("total_visiteurs"),
        func.avg(Frequentation.visiteurs).label("moyenne_visiteurs"),
    )

    result = db.execute(stmt).one()

    # Extraction des valeurs calculées à partir de result
    nb_obs = result.nb_observations or 0
    total_vis = result.total_visiteurs or 0
    moy_vis = float(result.moyenne_visiteurs) if result.moyenne_visiteurs is not None else 0.0

    return {
        "nb_observations": nb_obs,
        "total_visiteurs": total_vis,
        "moyenne_visiteurs": round(moy_vis, 2),
    }
    
   