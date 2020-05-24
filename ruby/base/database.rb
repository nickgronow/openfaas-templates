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

  def find(table, **where)
    where_sql = where.keys.map.with_index do |column, i|
      type = where[column].is_a?(String) ? 'text' : 'integer'
      "#{column} = $#{i+1}::#{type}"
    end.join(' AND ')
    first("SELECT * FROM #{table} WHERE #{where_sql}", *where.values)
  end
end

