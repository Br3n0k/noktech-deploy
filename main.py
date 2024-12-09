#!/usr/bin/env python
import sys
from src.deploy_client import main as deploy_client_main
from src.i18n import I18n


def main():
    i18n = I18n()

    if len(sys.argv) > 1:
        if sys.argv[1] in ["--lang", "-l"]:
            if len(sys.argv) > 2 and i18n.change_language(sys.argv[2]):
                print(
                    i18n.get("language.changed").format(
                        i18n.SUPPORTED_LANGUAGES[sys.argv[2]]
                    )
                )
                sys.exit(0)
            else:
                i18n.show_language_menu()
                sys.exit(1)

    try:
        deploy_client_main()
    except KeyboardInterrupt:
        print(i18n.get("error.cancelled"))
        sys.exit(1)
    except Exception as e:
        print(i18n.get("error.deploy").format(str(e)))
        sys.exit(1)


if __name__ == "__main__":
    main()
