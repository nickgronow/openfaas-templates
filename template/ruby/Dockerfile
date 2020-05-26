FROM openfaas/of-watchdog:0.7.2 as watchdog

FROM ruby:2.6.5-slim-stretch

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
RUN apt-get update \
  && apt-get install -qy --no-install-recommends ${ADDITIONAL_PACKAGE}

WORKDIR /home/app

RUN apt-get install -qy build-essential
RUN apt-get install -qy libpq-dev

COPY index.rb .
COPY Gemfile .
RUN bundle install

RUN mkdir -p /home/app/function
COPY function/Gemfile function/Gemfile
WORKDIR /home/app/function

RUN bundle install --without development

# Create a non-root user
RUN addgroup --system app \
    && adduser --system --ingroup app app

COPY function .
COPY base ../base

RUN chown app:app -R /home/app

USER app

WORKDIR /home/app

ENV fprocess="ruby index.rb"
EXPOSE 8080

HEALTHCHECK --interval=2s CMD [ -e /tmp/.lock ] || exit 1

ENV upstream_url="http://127.0.0.1:5000"
ENV mode="http"

ARG commit
ENV COMMIT_SHA=$commit

ARG environment
ENV APP_ENV=$environment

CMD ["fwatchdog"]
