from test_system.apps.teams.models import Team


def create_demo_team(organization):
    """Creates demo team for demonstration alongside the demo org."""

    if organization.is_demo:
        Team.objects.create(
            title="Demo-Team",
            description="Team for demonstration purposes.",
            organization=organization,
        )
