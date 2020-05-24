# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

require_relative 'function/handler'

require 'sinatra'
require 'raven'

# Capture output
$stdout.sync = true

set :port, 5000
set :bind, '0.0.0.0'

# Sentry configuration
Raven.configure do |config|
  config.dsn = 'https://98e7d91547aa4a5d86e6196dc99e2142@o71452.ingest.sentry.io/5223203'
  config.current_environment = ENV['APP_ENV']
  config.environments = %w[development production]
  config.release = ENV['COMMIT_SHA']
  config.processors -= [Raven::Processor::PostData] # Send POST data
  config.tags = {
    project: ENV['WOV_PROJECT'],
    cloud_function: ENV['WOV_FUNCTION']
  }
end
use Raven::Rack

post '/*' do
  response = Handler.new(request.body, request.env).run

  [response[:code], response[:headers], response[:body]]
end
