
# ====== Stage 1: Build ======
FROM gradle:8.5-jdk17-alpine AS builder
WORKDIR /home/gradle/project

# Copy Gradle files first to leverage Docker layer caching
COPY build.gradle settings.gradle gradlew gradlew.bat ./
COPY src ./src

# Ensure gradle wrapper is executable (if present)
RUN chmod +x gradlew || true

# Build the project; produce the fat JAR under build/libs/
# Use --no-daemon to prevent background processes in Docker
RUN gradle clean build -x test --no-daemon

# ====== Stage 2: Runtime ======
FROM amazoncorretto:17.0.7-alpine
# Create non-root user
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

WORKDIR /app

# Copy the built jar from the builder stage.
# Adjust the artifact name if your JAR has a different name:
# For Spring Boot default, it's often <project-name>-<version>.jar
# We pick the only .jar produced to avoid hardcoding the version.
COPY --from=builder /home/gradle/project/build/libs/*.jar /app/app.jar

# Expose port if your app runs on 8080 (check application.yml)
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
