# Use Node.js LTS (Long Term Support) version
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set build-time arguments for environment variables
ARG NEXT_PUBLIC_API_URL
ARG ACCESS_TOKEN

# Set environment variables
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV ACCESS_TOKEN=$ACCESS_TOKEN

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 