require 'test_helper'

class ArticlesControllerTest < ActionController::TestCase

  test "love article" do

    @article = articles(:android)

    get :love, :id => @article.id

    assert_response :success
    assert_true @article.

  end

end