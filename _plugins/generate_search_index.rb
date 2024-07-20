require 'json'
require 'nokogiri'
require 'jieba_rb'

class SearchIndexGenerator < Jekyll::Generator
  safe true

  def generate(site)
    puts "Generating search index..."

    jieba = JiebaRb::Keyword.new

    items = (site.pages + site.posts.docs).map do |page|
      if page.is_a?(Jekyll::Page)
        title = page.data['title']
        content = Nokogiri::HTML(page.content).text
        url = page.url
      elsif page.is_a?(Jekyll::Document)
        title = page.data['title']
        content = Nokogiri::HTML(page.content).text
        url = page.url
      else
        # 处理页面和文档之外的情况可以用作调试
        title, content, url = nil, nil, nil
      end

      # 确保 title 和 content 不为 nil
      title = "Untitled" if title.nil? || title.strip.empty?
      content = "No content available" if content.nil? || content.strip.empty?

      puts "Processing page: #{title}" # 添加日志以查看具体页面

      {
        "title" => jieba.extract(title, 10).map { |word| word[0] }.join(' '),
        "url" => url,
        "content" => jieba.extract(content, 50).map { |word| word[0] }.join(' ')
      }
    end

    File.open(File.join(site.dest, 'search.json'), 'w') do |file|
      file.write(items.to_json)
    end

    puts "Search index generated."
  end
end