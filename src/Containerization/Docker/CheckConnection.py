
# Test docker connection
import docker
try:
    client = docker.from_env()
    data = client.images.list(name="*ibeam*")

except Exception as e:
    logger.error(f"Error connecting to docker: {e}")
    raise e

else:
    logger.info(f"Connected to docker")

if not data:
    client.images.pull(IBKR_REST_CONTAINER_IMAGE, tag="latest")
    logger.info(f"Pulled {IBKR_REST_CONTAINER_IMAGE} image")

