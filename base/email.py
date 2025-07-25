# myapp/email.py

from djoser.email import ActivationEmail
from django.conf import settings


class AwesomeActivationEmail(ActivationEmail):
    template_name = "email/activation.html"
    subject_template_name = None  # get_subject

    def get_subject(self):
        site_name = getattr(settings, "DJOSER", {}).get(
            "EMAIL_FRONTEND_SITE_NAME", "Assessify"
        )
        return f"Activate your {site_name} account"

    def get_context_data(self):
        context = super().get_context_data()

        context.update(
            {
                "site_name": getattr(settings, "DJOSER", {}).get(
                    "EMAIL_FRONTEND_SITE_NAME", "Assessify"
                ),
            }
        )

        if "uid" in context and "token" in context:
            frontend_domain = getattr(settings, "DJOSER", {}).get(
                "EMAIL_FRONTEND_DOMAIN", "localhost:3000"
            )
            activation_path = getattr(settings, "DJOSER", {}).get(
                "ACTIVATION_URL", "auth/activate/{uid}/{token}"
            )

            formatted_path = activation_path.format(
                uid=context["uid"], token=context["token"]
            )

            protocol = "https" if not settings.DEBUG else "http"
            context["activation_url"] = (
                f"{protocol}://{frontend_domain}/{formatted_path}"
            )

        return context
