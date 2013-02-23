class ApplicationController < ActionController::Base
  
  private

  def logged_out?
    current_user.nil?
  end

  def logged_in?
    not current_user.nil?
  end

  def current_user
    begin
      @current_user ||= User.find(session[:user_id]) if session[:user_id]
    rescue
      redirect_to log_in_path
    end
  end
  
  helper_method :current_user
  helper_method :logged_in?
  helper_method :logged_out?
end


