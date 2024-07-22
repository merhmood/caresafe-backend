# Nginx with Certbot
FROM nginx:alpine

# # Install Certbot
# RUN apk add --no-cache certbot certbot-nginx

# # Copy Nginx configuration file
# COPY nginx.conf /etc/nginx/nginx.conf

# # Create directory for Certbot challenge
# RUN mkdir -p /var/www/certbot

# Expose ports
EXPOSE 80
EXPOSE 443

# Start Nginx
CMD ["sh", "-c", "nginx -g 'daemon off;'"]