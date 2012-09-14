require 'test_helper'

class StreamsControllerTest < ActionController::TestCase

  test "Get Stream" do

    @request.session[:user_id] = users(:Yves).user_id

    get :index, :format => :json
    assert_response :success
    assert_not_nil assigns(:articles)
  end

end