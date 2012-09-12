$:.unshift File.join(File.dirname(__FILE__),'..','lib')

require 'test/unit'
require 'google_reader'

class GoogleReaderTest < Test::Unit::TestCase
  
  def test_get_feeds
    reader = GoogleReader.new('nmaurer.dev@gmail.com', 'zs2.J+zg4.J09')
    puts reader.get_feeds
  end
  
end
