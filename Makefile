streamlit:
	-@streamlit run smard/frontend/app.py --server.port=8080 --server.address=0.0.0.0

run_api:
	uvicorn wildfaire.api.fast:app --reload
