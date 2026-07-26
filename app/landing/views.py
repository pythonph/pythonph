from django.shortcuts import render

from app.organisation.models import Commitee


def index(request):
    committees = Commitee.available_objects.prefetch_related("volunteers")
    python_hour = [
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "Let's create animated Memes using Python and MoviePy",
            "date": "Thursday, October 13, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_1.png",
        },
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "API Development using Flask",
            "date": "Thursday, October 20, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_2.png",
        },
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "Data Science using Python!",
            "date": "Thursday, October 27, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_3.png",
        },
    ]

    board_of_trustees = [
        {
            "name": "Zorex Salvo",
            "position": "President",
            "image": "landing/assets/img/people/zorex.jpg",
        },
        {
            "name": "Freilla Mae Espinola",
            "position": "Director of Operations",
            "image": "landing/assets/img/people/freilla.png",
        },
        {
            "name": "Sony Valdez",
            "position": "Director of Community Relations",
            "image": "landing/assets/img/people/shuny.jpg",
        },
        {
            "name": "Ciara Bautista",
            "position": "Treasurer",
            "image": "landing/assets/img/people/ciara.jpg",
        },
        {
            "name": "Rodney Lei Estrada",
            "position": "Board of Trustee and Corporate Secretary",
            "image": "landing/assets/img/people/rodney.jpg",
        },
        {
            "name": "Cyrus Mante",
            "position": "Board of Trustee",
            "image": "landing/assets/img/people/cyrus.jpg",
        },
        {
            "name": "Matt Lebrun",
            "position": "Director of Volunteer Training & Engagement",
            "image": "landing/assets/img/people/matt.jpg",
        },
        {
            "name": "Micaela Reyes",
            "position": "Board of Trustee",
            "image": "landing/assets/img/people/micaela.jpg",
        },
    ]

    directors = [
        {
            "name": "Lalaine Diok",
            "position": "Director of Marketing",
            "image": "landing/assets/img/people/lalaine.jpg",
        },
        {
            "name": "Alex Reyes",
            "position": "Director of Design",
            "image": "landing/assets/img/people/alex.jpg",
        },
        {
            "name": "Kyle Shaun Aquino",
            "position": "Director of Engineering",
            "image": "landing/assets/img/people/kyle.jpg",
        },
        {
            "name": "Romar Mayer Micabalo",
            "position": "Director of Outreach & Diversity",
            "image": "landing/assets/img/people/romar.jpg",
        },
    ]

    return render(
        request,
        "landing/index.html",
        {
            "committees": committees,
            "python_hour": python_hour,
            "board_of_trustees": board_of_trustees,
            "directors": directors,
        },
    )
