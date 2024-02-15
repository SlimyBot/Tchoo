# Builder image
FROM node:20-alpine as builder

WORKDIR /app

COPY Tchoo_web/package.json ./

RUN npm install

COPY Tchoo_web/ ./

RUN npm run build

# Production image
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/ /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
