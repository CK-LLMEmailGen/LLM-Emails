# Stage 1: Build React App
FROM node:14 as builder
WORKDIR /code
COPY templates/react-app/ /code
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Build FastAPI backend and create final image
FROM python:3.11 as final
WORKDIR /code
COPY --from=builder /code/build /code/static
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
