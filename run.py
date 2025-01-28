from playwright.sync_api import sync_playwright
import time

def delete_all_tweets():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 登录Twitter
            page.goto("https://twitter.com/login")
            print("请在浏览器中手动登录Twitter...")
            
            # 等待用户手动登录，直到检测到主页元素
            page.wait_for_selector('[data-testid="primaryColumn"]')
            print("登录成功！")
            
            # 访问个人资料页面（需要等待一下确保登录状态已完全加载）
            time.sleep(3)
            # 点击个人头像进入个人资料页
            page.click('[data-testid="AppTabBar_Profile_Link"]')
            time.sleep(3)  # 等待个人资料页面加载
            
            while True:
                try:
                    # 查找推文
                    tweets = page.query_selector_all('[data-testid="tweet"]')
                    
                    if not tweets:
                        print("没有找到更多推文")
                        break
                    
                    for tweet in tweets:
                        try:
                            # 点击更多按钮
                            more_button = tweet.query_selector('[data-testid="caret"]')
                            if more_button:
                                more_button.click()
                                time.sleep(1)
                            
                            # 点击删除按钮
                            delete_button = page.wait_for_selector(
                                '[data-testid="Dropdown"] [role="menuitem"]',
                                timeout=5000
                            )
                            if delete_button:
                                delete_button.click()
                                time.sleep(1)
                            
                            # 确认删除
                            confirm_button = page.wait_for_selector(
                                '[data-testid="confirmationSheetConfirm"]',
                                timeout=5000
                            )
                            if confirm_button:
                                confirm_button.click()
                                print("成功删除一条推文")
                                time.sleep(2)
                            
                        except Exception as e:
                            print(f"删除推文时出错: {str(e)}")
                            continue
                    
                    # 刷新页面以加载更多推文
                    page.reload()
                    time.sleep(3)
                    
                except Exception as e:
                    print(f"发生错误: {str(e)}")
                    page.reload()
                    time.sleep(5)
                    continue
                
        finally:
            # 完成后关闭浏览器
            browser.close()
            print("操作完成！")

if __name__ == "__main__":
    delete_all_tweets()
