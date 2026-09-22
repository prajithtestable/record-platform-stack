FROM node:22-alpine
WORKDIR /app
COPY backend-service-a/package*.json ./
RUN npm install --omit=dev
COPY backend-service-a/. .
COPY shared /app/shared
ENV NODE_ENV=production
EXPOSE 3001 50051
CMD ["node", "src/index.js"]
