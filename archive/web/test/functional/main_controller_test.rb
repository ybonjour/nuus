require 'test_helper'

class MainControllerTest < ActionController::TestCase
  test "get stream when session-user does not exist any more" do

    @request.session[:user_id] = 'bullshit'

    get :stream
    assert_redirected_to log_in_path
  end

  test "get stream when logged out" do
    get :stream
    assert_redirected_to log_in_path
  end
end
