require 'test/unit'

class GoogleApiGateway < Test::Unit::TestCase
  def test_authenticate
    
    gateway = GoogleApiGateway.new
    assert_not_nil gateway
    
  end
end
