require 'test_helper'

class ArticleTest < ActiveSupport::TestCase

  test "find" do
    articles = Article.all
    assert_equal 4, articles.size
  end

end