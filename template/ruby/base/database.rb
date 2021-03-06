require 'pg'

class Database
  attr_reader :connection

  def initialize(**options)
    @connection = PG.connect(
      host: options[:host],
      port: 5432,
      dbname: options[:db],
      user: options[:user],
      password: options[:password]
    )
    @connection.type_map_for_results =
      PG::BasicTypeMapForResults.new @connection
    @connection.type_map_for_queries =
      PG::BasicTypeMapForQueries.new @connection
  end

  def query(sql, *params)
    result = connection.exec_params(sql, params)
    result.field_name_type = :symbol
    result
  end

  def first(sql, *params)
    query(sql, *params)&.first
  end

  def last(sql, *params)
    query(sql, *params)&.last
  end

  def detect_type(value)
    return 'integer' if value.is_a?(Integer)

    if value.is_a?(String)
      return /\A\d+\z/.match(value) ? 'integer' : 'text'
    end
    'text'
  end

  def find(table, **where)
    where_sql = where.keys.map.with_index do |column, i|
      type = detect_type(where[column])
      "#{column} = $#{i+1}::#{type}"
    end.join(' AND ')
    first(
      "SELECT * FROM #{table} WHERE #{where_sql} ORDER BY id DESC LIMIT 1",
      *where.values
    )
  end
end

