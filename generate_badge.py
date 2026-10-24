import requests
from pathlib import Path
from html import escape

USER_ID = "68848"

BASE_URL = "https://hackatime.hackclub.com/api/v1"


def get_stats():
    response = requests.get(
        f"{BASE_URL}/users/{USER_ID}/stats"
    )
    response.raise_for_status()

    return response.json()["data"]


def get_projects():
    response = requests.get(
        f"{BASE_URL}/users/{USER_ID}/projects/details"
    )
    response.raise_for_status()

    return response.json()["projects"]


def generate_badge():

    stats = get_stats()
    projects = get_projects()

    total_time = stats["human_readable_total"]

    top_language = max(
        stats["languages"],
        key=lambda language: language["total_seconds"]
    )

    top_project = max(
        projects,
        key=lambda project: project["total_seconds"]
    )

    total_time = escape(total_time)
    language = escape(top_language["name"])
    project = escape(top_project["name"])

    project_url = escape(
        top_project.get("repo_url") or "",
        quote=True
    )

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="860"
         height="104"
         viewBox="0 0 860 104">

      <defs>
        <linearGradient id="glass">
          <stop offset="0%" stop-color="#ffffff" stop-opacity=".18"/>
          <stop offset="100%" stop-color="#ffffff" stop-opacity=".04"/>
        </linearGradient>

        <linearGradient id="accent">
          <stop offset="0%" stop-color="#a78bfa"/>
          <stop offset="100%" stop-color="#67e8f9"/>
        </linearGradient>
      </defs>

      <rect x="1" y="1"
            width="858" height="102"
            rx="18"
            fill="url(#glass)"
            stroke="#ffffff"
            stroke-opacity=".25"/>

      <rect x="17" y="17"
            width="3" height="70"
            rx="2"
            fill="url(#accent)"/>

      <g font-family="Arial, sans-serif">

        <text x="36" y="31"
              font-size="10"
              fill="#8b93a7">
          HACKATIME
        </text>

        <text x="36" y="57"
              font-size="17"
              font-weight="bold"
              fill="#e8ecf8">
          {total_time}
        </text>

        <text x="36" y="77"
              font-size="10"
              fill="#8b93a7">
          TOTAL CODING TIME
        </text>


        <line x1="275" y1="21"
              x2="275" y2="83"
              stroke="#8b93a7"
              stroke-opacity=".25"/>

        <text x="302" y="31"
              font-size="10"
              fill="#8b93a7">
          TOP LANGUAGE
        </text>

        <text x="302" y="57"
              font-size="17"
              font-weight="bold"
              fill="#e8ecf8">
          {language}
        </text>

        <text x="302" y="77"
              font-size="10"
              fill="#8b93a7">
          MOST TRACKED LANGUAGE
        </text>


        <line x1="555" y1="21"
              x2="555" y2="83"
              stroke="#8b93a7"
              stroke-opacity=".25"/>

        <text x="584" y="31"
              font-size="10"
              fill="#8b93a7">
          TOP PROJECT
        </text>

        <a href="{project_url}">
          <text x="584" y="57"
                font-size="15"
                font-weight="bold"
                fill="#e8ecf8">
            {project}
          </text>
        </a>

        <text x="584" y="77"
              font-size="10"
              fill="#8b93a7">
          MOST TRACKED PROJECT
        </text>

      </g>
    </svg>
    """

    output = Path("assets/hackatime-glass.svg")
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(svg, encoding="utf-8")

    print("Badge generated successfully!")


if __name__ == "__main__":
    generate_badge()