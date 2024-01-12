from fastapi import APIRouter, status, Depends, HTTPException
import utils
import requests
from config import config

router = APIRouter()

@router.get('/weather/current/{town}', status_code=status.HTTP_201_CREATED )
async def get_current_weather(
    town: str,
    payload: dict = Depends(utils.validate_access_token)):

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring= {"q":f"{town}"}

    headers = {
	"X-RapidAPI-Key": config.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

@router.get('/weather/future/{town}/{days}', status_code=status.HTTP_201_CREATED )
async def get_current_weather(
    town: str,
    days: str,
    payload: dict = Depends(utils.validate_access_token)):

    if int(days) > 7:
        days = "7"

    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring= {"q":f"{town}", "days":f"{days}"}

    headers = {
	"X-RapidAPI-Key": config.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()