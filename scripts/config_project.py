from scripts import install_requirements,alembic_revision,alembic_upgrade, create_dotenv

def main():

    install_requirements.main()
    create_dotenv.main()
    alembic_revision.main()
    alembic_upgrade.main()

if __name__ == "__main__":
    main()
