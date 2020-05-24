require 'json'
require_relative './database'

class ActionHandler
  attr_reader :body, :headers, :db

  def initialize(body, headers)
    @body = JSON.parse(body.string, symbolize_names: true)
    @headers = headers
    log("ACTION: #{action} STARTED")
  end

  def initdb(namespace)
    return if testing

    @db = Database.new(
      host: secret('wov-db-host'),
      dbname: secret("#{namespace}-db-name"),
      user: secret("#{namespace}-db-user"),
      password: secret("#{namespace}-db-pw")
    )
  end

  def log(message)
    return if testing

    puts message
  end

  def testing
    ENV['RUBY_ENV'] == 'test'
  end

  def action
    body.dig(:action, :name)
  end

  def input(key)
    body.dig(:input, key)
  end

  def hasura(key)
    hasura_key = "x-hasura-#{key}".to_sym
    body.dig(:session_variables, hasura_key)
  end

  def response(payload)
    {
      body: payload.to_json,
      headers: {'content-type' => 'application/json'},
      code: 200
    }
  end

  def secret(name)
    path = "/var/openfaas/secrets/#{name}"
    return nil unless File.exist?(path)

    File.read(path).gsub("\n", '')
  end
end
