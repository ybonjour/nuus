require 'test_helper'

class SessionsControllerTest < ActionController::TestCase
  test "create session" do
    get :create
    assert_response :success
  end

end
