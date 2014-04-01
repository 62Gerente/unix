begin
  require 'rubygems'
rescue LoadError
  $stderr.puts "Please install rubygems before continuing"
end

begin
  require 'slim'
  require 'slim/command'

  Slim::Command.new(ARGV).run
rescue LoadError
  $stderr.puts "Please run `gem install slim` before continuing"
end