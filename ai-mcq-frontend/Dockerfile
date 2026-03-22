FROM node:20-bookworm-slim

WORKDIR /app

# Copy package files first for better cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Required so Vite works properly inside Docker on Windows
ENV CHOKIDAR_USEPOLLING=true

# Start Vite dev server and expose to network
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]