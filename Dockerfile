FROM postgres:latest
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=sparkifydb
RUN docker run -d -p 5432:5432 --name sparkifydb -e POSTGRES_PASSWORD=mysecretpassword postgres
RUN docker exec -it my-postgres bash
CMD CREATE DATABASE sparkifydb
