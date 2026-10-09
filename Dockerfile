# CPU image (works anywhere). For a GPU, start from an NVIDIA CUDA PyTorch base image instead and run with --gpus all.
FROM python:3.12-slim
WORKDIR /dex
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server ./server
COPY model ./model
ENV DEX_MODEL=/dex/model DEX_HOST=0.0.0.0 DEX_DEVICE=cpu HF_HUB_OFFLINE=1
EXPOSE 18766
CMD ["python", "server/dex_server.py", "18766"]
