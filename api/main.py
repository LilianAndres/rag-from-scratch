import uvicorn

from app.config.settings import AppSettings


def main() -> None:
    settings = AppSettings()

    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.env != "prod",
    )


if __name__ == "__main__":
    main()