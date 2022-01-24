ARG SERVER_IMAGE_NAME=rclsilver/prenoms-server
ARG SERVER_IMAGE_TAG=latest
ARG FRONTEND_IMAGE_NAME=rclsilver/prenoms-frontend
ARG FRONTEND_IMAGE_TAG=latest

FROM ${FRONTEND_IMAGE_NAME}:${FRONTEND_IMAGE_TAG} AS frontend
FROM ${SERVER_IMAGE_NAME}:${SERVER_IMAGE_TAG} as server

USER root:root

RUN set -eux && \
    apk update && \
    apk add nginx

# DEBUG
RUN set -eux && \
    pip install supervisor

# Copy the frontend
COPY --from=frontend /usr/share/nginx/html /usr/share/nginx/html/

# Copy the nginx configuration
COPY ./nginx/nginx.conf.production /etc/nginx/nginx.conf

# Copy the supervisord configuration
COPY ./supervisor/supervisord.conf /etc/supervisord.conf

# Start supervisor
CMD [ "/usr/local/bin/supervisord", "--configuration=/etc/supervisord.conf" ]
