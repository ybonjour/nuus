require 'test_helper'

class MainControllerTest < ActionController::TestCase
  test "get stream when session-user does not exist any more" do

    @request.session[:user_id] = 'bullshit'

    get :stream
    assert_redirected_to :controller => :sessions, :action => :new
  end

  test "get stream when logged out" do
    get :stream
    assert_redirected_to :controller => :sessions, :action => :new
  end
end
