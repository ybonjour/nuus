require 'test_helper'

class UserTest < ActiveSupport::TestCase
  test "save user" do
    
    user = User.new
    user.email = 'test@nuus.ch'
    user.password = 'test'
    
    assert user.save, user.errors
    
  end
  
  test "find user by email" do
    
    users = User.where(:email => 'yves@nuus.ch')
    
    assert_equal 1, users.size
  end
  
  test "find user by wrong email" do
    
    users = User.where(:email => 'if@nuus.ch')
    
    assert_equal 0, users.size
  end
  
end
