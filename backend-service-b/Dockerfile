FROM node:22-alpine
WORKDIR /app
COPY backend-service-b/package*.json ./
RUN npm install --omit=dev
COPY backend-service-b/. .
COPY shared /app/shared
ENV NODE_ENV=production
CMD ["node", "src/index.js"]
